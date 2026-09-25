package com.setu.core.d.mitigation.repository;

import com.setu.core.d.mitigation.entity.MitigationStrategy;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

public interface MitigationStrategyRepository extends JpaRepository<MitigationStrategy, Long> {
    Optional<MitigationStrategy> findTopByProjectNameAndSessionIdOrderByStrategyIdDesc(
            String projectName, Integer sessionId);
    List<MitigationStrategy> findByProjectNameAndSessionIdOrderByStrategyIdAsc(
            String projectName, Integer sessionId);
}