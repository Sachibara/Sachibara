package com.sachibara.inventory;
import java.util.List;import org.springframework.data.jpa.repository.JpaRepository;
public interface MovementRepository extends JpaRepository<Movement,Long>{List<Movement> findTop100ByProductIdOrderByCreatedDesc(Long productId);}
