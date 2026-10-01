<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration {
    public function up(): void { Schema::create('expenses', function(Blueprint $table) {
        $table->id(); $table->string('description',120); $table->string('category',30);
        $table->unsignedInteger('amount_cents'); $table->date('spent_on')->index(); $table->timestamps();
    }); }
    public function down(): void { Schema::dropIfExists('expenses'); }
};
