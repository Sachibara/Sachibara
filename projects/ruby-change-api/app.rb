require 'sinatra/base'
require 'sqlite3'
require 'json'
require 'fileutils'
class ChangeAPI < Sinatra::Base
  set :bind, '127.0.0.1'
  set :port, 4567
  set :show_exceptions, false
  set :host_authorization, { permitted_hosts: ['localhost', '127.0.0.1', 'example.org'] }
  TOKEN = ENV.fetch('CHANGE_API_TOKEN') { raise 'Set CHANGE_API_TOKEN before starting the API' }
  raise 'CHANGE_API_TOKEN must be at least 32 characters' if TOKEN.bytesize < 32
  TRANSITIONS = {'Draft'=>['Approved','Rejected'], 'Approved'=>['Implemented'], 'Rejected'=>[], 'Implemented'=>[]}.freeze
  DB_PATH = ENV.fetch('CHANGE_DB_PATH', File.join(__dir__, 'data', 'changes.sqlite'))
  FileUtils.mkdir_p(File.dirname(DB_PATH))
  db=SQLite3::Database.new(DB_PATH)
  db.execute("CREATE TABLE IF NOT EXISTS changes (id INTEGER PRIMARY KEY, title TEXT NOT NULL, risk TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Draft', created_at TEXT NOT NULL)")
  db.close
  helpers do
    def database
      @db ||= SQLite3::Database.new(DB_PATH).tap { |db| db.results_as_hash=true; db.busy_timeout=5000 }
    end
    def failure(code,message); halt code, JSON.generate({error:message}); end
    def payload
      failure(413,'Payload too large') if request.content_length.to_i > 16384
      raw=request.body.read(16385); failure(413,'Payload too large') if raw.bytesize>16384
      value=JSON.parse(raw); failure(400,'Body must be an object') unless value.is_a?(Hash); value
    rescue JSON::ParserError
      failure(400,'Invalid JSON')
    end
    def record(id)
      failure(400,'Invalid ID') unless id.match?(/\A[1-9]\d*\z/)
      row=database.get_first_row('SELECT * FROM changes WHERE id=?',id.to_i); failure(404,'Change not found') unless row; row
    end
  end
  before do
    content_type :json
    headers 'Cache-Control'=>'no-store', 'X-Content-Type-Options'=>'nosniff'
    expected='Bearer '+TOKEN; supplied=request.env['HTTP_AUTHORIZATION'].to_s
    failure(401,'Bearer token required') unless supplied.bytesize==expected.bytesize && Rack::Utils.secure_compare(supplied,expected)
  end
  after { @db&.close }
  get('/health') { JSON.generate({status:'ok'}) }
  get('/changes') { JSON.generate(database.execute('SELECT * FROM changes ORDER BY id DESC LIMIT 500')) }
  post '/changes' do
    data=payload; title=data['title']; risk=data['risk']
    failure(422,'Title (1–120 characters) and Low/Medium/High risk required') unless title.is_a?(String) && title.strip.length.between?(1,120) && ['Low','Medium','High'].include?(risk)
    database.execute('INSERT INTO changes(title,risk,created_at) VALUES (?,?,?)',[title.strip,risk,Time.now.utc.strftime('%Y-%m-%dT%H:%M:%SZ')])
    status 201; JSON.generate(record(database.last_insert_row_id.to_s))
  end
  patch '/changes/:id/status' do
    row=record(params[:id]); next_status=payload['status']
    failure(409,'Invalid transition') unless TRANSITIONS.fetch(row['status']).include?(next_status)
    database.execute('UPDATE changes SET status=? WHERE id=? AND status=?',[next_status,row['id'],row['status']])
    failure(409,'Record changed; reload and retry') if database.changes.zero?
    JSON.generate(record(params[:id]))
  end
  error { status 500; JSON.generate({error:'Internal server error'}) }
  run! if app_file == $PROGRAM_NAME
end
