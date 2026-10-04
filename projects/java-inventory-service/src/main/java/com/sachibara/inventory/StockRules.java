package com.sachibara.inventory;
import java.util.Locale;
public final class StockRules {
    private StockRules() {}
    public static String sku(String value){if(value==null||!value.trim().matches("[A-Za-z0-9_-]{1,40}"))throw new IllegalArgumentException("SKU must be 1–40 letters, digits, hyphens or underscores.");return value.trim().toUpperCase(Locale.ROOT);}
    public static int apply(int current,int delta){long next=(long)current+delta;if(delta==0||next<0||next>1_000_000)throw new IllegalArgumentException("Adjustment must be nonzero and stock must remain between 0 and 1,000,000.");return (int)next;}
}
