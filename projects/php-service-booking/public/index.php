<?php
declare(strict_types=1);
session_start(['cookie_httponly'=>true,'cookie_samesite'=>'Lax']);
header('X-Content-Type-Options: nosniff');
header("Content-Security-Policy: default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'");
$dir=dirname(__DIR__).'/data'; if(!is_dir($dir))mkdir($dir,0700,true);
$db=new PDO('sqlite:'.$dir.'/bookings.sqlite');$db->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
$db->exec('PRAGMA busy_timeout=5000');
$db->exec("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, client TEXT NOT NULL, service TEXT NOT NULL, date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Requested')");
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));
function e(string $s):string{return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
$error='';
if($_SERVER['REQUEST_METHOD']==='POST') {
    if(!is_string($_POST['csrf']??null)||!hash_equals($_SESSION['csrf'],$_POST['csrf'])){http_response_code(403);exit('Invalid request token.');}
    try {
        if(($_POST['action']??'')==='create'){
            $client=trim((string)($_POST['client']??''));$service=(string)($_POST['service']??'');$date=(string)($_POST['date']??'');
            $parsed=DateTimeImmutable::createFromFormat('!Y-m-d',$date);
            if($client===''||strlen($client)>100||!in_array($service,['Network Setup','PC Repair','Remote Support'],true)||!$parsed||$parsed->format('Y-m-d')!==$date||$date<date('Y-m-d'))throw new InvalidArgumentException('Enter a client, valid service and a current or future date.');
            $stmt=$db->prepare('INSERT INTO bookings(client,service,date) VALUES (?,?,?)');$stmt->execute([$client,$service,$date]);
        } elseif(($_POST['action']??'')==='status') {
            $status=(string)($_POST['status']??'');$id=filter_var($_POST['id']??'',FILTER_VALIDATE_INT);
            if(!$id||!in_array($status,['Requested','Confirmed','Completed','Cancelled'],true))throw new InvalidArgumentException('Invalid status update.');
            $stmt=$db->prepare('UPDATE bookings SET status=? WHERE id=?');$stmt->execute([$status,$id]);
        } else throw new InvalidArgumentException('Unknown action.');
        header('Location: /',true,303);exit;
    } catch(InvalidArgumentException $ex){$error=$ex->getMessage();} catch(PDOException $ex){error_log($ex->getMessage());$error='Unable to save booking. Try again.';}
}
$query=trim((string)($_GET['q']??''));$stmt=$db->prepare('SELECT * FROM bookings WHERE client LIKE ? OR service LIKE ? ORDER BY date,id');$stmt->execute(['%'.$query.'%','%'.$query.'%']);$rows=$stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ServiceSlot</title><link rel="stylesheet" href="/style.css"></head><body><main><header><div><span class="eyebrow">Sachibara / PHP lab</span><h1>ServiceSlot</h1><p class="muted">Organize technical service requests and appointment dates.</p></div><span class="badge">PHP + PDO SQLite</span></header>
<?php if($error): ?><p class="error" role="alert"><?=e($error)?></p><?php endif; ?>
<form method="post" class="inline"><input type="hidden" name="csrf" value="<?=e($_SESSION['csrf'])?>"><input type="hidden" name="action" value="create"><label>Client<br><input name="client" required maxlength="100"></label><label>Service<br><select name="service"><option>Network Setup</option><option>PC Repair</option><option>Remote Support</option></select></label><label>Date<br><input name="date" type="date" min="<?=date('Y-m-d')?>" required></label><button>Request booking</button></form>
<form method="get" class="inline"><label>Search client or service<br><input name="q" value="<?=e($query)?>"></label><button class="secondary">Search</button><a href="/">Clear</a></form>
<section class="panel table-wrap"><table><thead><tr><th>Client</th><th>Service</th><th>Date</th><th>Status</th><th>Update</th></tr></thead><tbody><?php foreach($rows as $r): ?><tr><td><?=e($r['client'])?></td><td><?=e($r['service'])?></td><td><?=e($r['date'])?></td><td><span class="badge"><?=e($r['status'])?></span></td><td><form method="post"><input type="hidden" name="csrf" value="<?=e($_SESSION['csrf'])?>"><input type="hidden" name="action" value="status"><input type="hidden" name="id" value="<?=(int)$r['id']?>"><label>Status for booking <?=(int)$r['id']?><br><select name="status"><?php foreach(['Requested','Confirmed','Completed','Cancelled'] as $s): ?><option <?= $s===$r['status']?'selected':''?>><?=e($s)?></option><?php endforeach; ?></select></label><button>Save</button></form></td></tr><?php endforeach; ?></tbody></table><?php if(!$rows): ?><p>No bookings found. Add your first request.</p><?php endif; ?></section><footer>Local single-operator demo · Prepared statements · CSRF tokens · Escaped output</footer></main></body></html>
