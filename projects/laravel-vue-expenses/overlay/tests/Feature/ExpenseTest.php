<?php
namespace Tests\Feature;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
class ExpenseTest extends TestCase {
    use RefreshDatabase;
    public function test_crud_and_validation(): void {
        $this->postJson('/expenses', ['description'=>'Cable','category'=>'Equipment','amount_cents'=>-1,'spent_on'=>'2026-10-01'])->assertUnprocessable();
        $row=$this->postJson('/expenses', ['description'=>'Cable','category'=>'Equipment','amount_cents'=>12550,'spent_on'=>'2026-10-01'])->assertCreated()->json();
        $this->getJson('/expenses')->assertJsonCount(1)->assertJsonFragment(['amount_cents'=>12550]);
        $this->putJson('/expenses/'.$row['id'], ['description'=>'Cable updated','category'=>'Equipment','amount_cents'=>10000,'spent_on'=>'2026-10-01'])->assertOk();
        $this->deleteJson('/expenses/'.$row['id'])->assertNoContent();
        $this->getJson('/expenses')->assertJsonCount(0);
    }
}
