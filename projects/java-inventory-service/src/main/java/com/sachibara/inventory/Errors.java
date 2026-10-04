package com.sachibara.inventory;
import java.util.Map;import org.springframework.web.bind.annotation.*;import org.springframework.http.*;import org.springframework.dao.DataIntegrityViolationException;import org.springframework.web.bind.MethodArgumentNotValidException;
@RestControllerAdvice public class Errors {
 @ExceptionHandler(IllegalArgumentException.class) ResponseEntity<?> bad(IllegalArgumentException e){return ResponseEntity.badRequest().body(Map.of("error",e.getMessage()));}
 @ExceptionHandler(MethodArgumentNotValidException.class) ResponseEntity<?> validation(MethodArgumentNotValidException e){return ResponseEntity.badRequest().body(Map.of("error","Check required fields and numeric limits."));}
 @ExceptionHandler(DataIntegrityViolationException.class) ResponseEntity<?> duplicate(){return ResponseEntity.status(409).body(Map.of("error","SKU already exists or data constraint failed."));}
}
