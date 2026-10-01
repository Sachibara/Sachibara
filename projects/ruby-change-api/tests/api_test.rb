ENV['CHANGE_API_TOKEN']='test-token-that-is-at-least-32-characters'
require 'tmpdir'
ENV['CHANGE_DB_PATH']=File.join(Dir.mktmpdir,'test.sqlite')
require 'minitest/autorun'
require 'rack/test'
require_relative '../app'
class ApiTest < Minitest::Test
  include Rack::Test::Methods
  def app; ChangeAPI; end
  def setup; header 'Authorization', 'Bearer '+ENV['CHANGE_API_TOKEN']; header 'Content-Type','application/json'; end
  def test_authentication; header 'Authorization',nil; get '/changes'; assert_equal 401,last_response.status; end
  def test_lifecycle
    post '/changes',JSON.generate({title:'Replace branch switch',risk:'High'}); assert_equal 201,last_response.status
    id=JSON.parse(last_response.body)['id']
    patch "/changes/#{id}/status",JSON.generate({status:'Implemented'}); assert_equal 409,last_response.status
    patch "/changes/#{id}/status",JSON.generate({status:'Approved'}); assert_equal 200,last_response.status
    patch "/changes/#{id}/status",JSON.generate({status:'Implemented'}); assert_equal 200,last_response.status
  end
  def test_invalid_json; post '/changes','{bad'; assert_equal 400,last_response.status; end
end
