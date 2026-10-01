<?php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ExpenseController;
Route::get('/', fn()=>view('app'));
Route::get('/expenses', [ExpenseController::class,'index']);
Route::post('/expenses', [ExpenseController::class,'store']);
Route::put('/expenses/{expense}', [ExpenseController::class,'update']);
Route::delete('/expenses/{expense}', [ExpenseController::class,'destroy']);
