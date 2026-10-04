import com.sachibara.inventory.StockRules;
public class StockRulesCheck {
 public static void main(String[] args){if(!StockRules.sku(" cable-1 ").equals("CABLE-1"))throw new AssertionError();if(StockRules.apply(10,-3)!=7)throw new AssertionError();for(int delta:new int[]{-11,0,Integer.MAX_VALUE}){try{StockRules.apply(10,delta);throw new AssertionError("Invalid adjustment accepted");}catch(IllegalArgumentException expected){}}try{StockRules.sku("bad\ncommand");throw new AssertionError();}catch(IllegalArgumentException expected){}System.out.println("Stock rules: normalization, debit, underflow, zero, overflow and invalid SKU passed.");}
}
