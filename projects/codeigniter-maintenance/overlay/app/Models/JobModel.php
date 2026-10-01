<?php
namespace App\Models;
use CodeIgniter\Model;
class JobModel extends Model {
    protected $table='jobs'; protected $primaryKey='id'; protected $allowedFields=['equipment','issue','priority','status'];
}
