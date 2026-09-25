package com.setu.core.e.risk.repository;

import com.setu.core.e.risk.entity.RiskScore;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;
import com.setu.core.e.risk.entity.RiskLevel;
import org.springframework.data.domain.Pageable;


public interface RiskScoreRepository extends JpaRepository<RiskScore, Long> {

    // Most recent score for a project
    Optional<RiskScore> findTopByProject_ProjectIdOrderByGeneratedAtDesc(Long projectId);

    List<RiskScore> findByProject_ProjectId(Long projectId);

    @org.springframework.data.jpa.repository.Query(
            "SELECT r FROM RiskScore r WHERE r.generatedAt = " +
                    "(SELECT MAX(r2.generatedAt) FROM RiskScore r2 WHERE r2.project = r.project) " +
                    "ORDER BY r.riskScoreValue DESC")
    List<RiskScore> findLatestScoresOrderedByValueDesc(Pageable pageable);

    long countByRiskLevel(RiskLevel riskLevel);
}