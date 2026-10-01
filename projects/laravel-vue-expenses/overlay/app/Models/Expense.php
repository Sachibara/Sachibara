<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class Expense extends Model {
    protected $fillable = ['description','category','amount_cents','spent_on'];
    protected $casts = ['amount_cents'=>'integer'];
}
