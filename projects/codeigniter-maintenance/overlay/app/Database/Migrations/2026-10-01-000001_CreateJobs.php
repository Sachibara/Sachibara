<?php
namespace App\Database\Migrations;
use CodeIgniter\Database\Migration;
class CreateJobs extends Migration {
    public function up() {
        $this->forge->addField(['id'=>['type'=>'INTEGER','auto_increment'=>true], 'equipment'=>['type'=>'VARCHAR','constraint'=>120],
            'issue'=>['type'=>'TEXT'], 'priority'=>['type'=>'VARCHAR','constraint'=>10], 'status'=>['type'=>'VARCHAR','constraint'=>20,'default'=>'Open']]);
        $this->forge->addKey('id',true); $this->forge->createTable('jobs');
    }
    public function down() { $this->forge->dropTable('jobs'); }
}
