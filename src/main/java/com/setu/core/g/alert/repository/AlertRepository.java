package com.setu.core.g.alert.repository;

import com.setu.core.g.alert.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AlertRepository extends JpaRepository<Alert, Long> {
    List<Alert> findByAcknowledgedFalseOrderByCreatedAtDesc();
    List<Alert> findByProject_ProjectIdOrderByCreatedAtDesc(Long projectId);
    long countByAcknowledgedFalse();
    long countBySeverityAndAcknowledgedFalse(com.setu.core.g.alert.entity.AlertSeverity severity);
}