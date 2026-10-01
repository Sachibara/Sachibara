<?php
namespace App\Http\Controllers;
use App\Models\Expense;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
class ExpenseController extends Controller {
    public function index() { return Expense::orderByDesc('spent_on')->orderByDesc('id')->get(); }
    private function validated(Request $request): array {
        return $request->validate(['description'=>'required|string|max:120', 'category'=>['required',Rule::in(['Travel','Equipment','Software','Other'])],
            'amount_cents'=>'required|integer|min:1|max:100000000', 'spent_on'=>'required|date_format:Y-m-d']);
    }
    public function store(Request $request) { return response()->json(Expense::create($this->validated($request)),201); }
    public function update(Request $request, Expense $expense) { $expense->update($this->validated($request)); return $expense; }
    public function destroy(Expense $expense) { $expense->delete(); return response()->noContent(); }
}
