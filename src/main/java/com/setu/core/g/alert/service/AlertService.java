package com.setu.core.g.alert.service;

import com.setu.core.c.project.entity.Project;
import com.setu.core.e.risk.entity.RiskLevel;
import com.setu.core.g.alert.dto.AlertDto;
import com.setu.core.g.alert.entity.Alert;
import com.setu.core.g.alert.entity.AlertSeverity;
import com.setu.core.g.alert.repository.AlertRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class AlertService {

    @Autowired
    private AlertRepository alertRepository;

    public void evaluateAndCreateAlert(Project project, RiskLevel riskLevel, Double riskScoreValue) {
        if (riskLevel == RiskLevel.HIGH || riskLevel == RiskLevel.CRITICAL) {
            Alert alert = new Alert();
            alert.setProject(project);
            alert.setSeverity(riskLevel == RiskLevel.CRITICAL ? AlertSeverity.CRITICAL : AlertSeverity.WARNING);
            alert.setMessage(String.format("Project '%s' flagged as %s risk (score: %.1f)",
                    project.getName(), riskLevel.name(), riskScoreValue));
            alertRepository.save(alert);
        }
    }

    public List<AlertDto> getActiveAlerts() {
        return alertRepository.findByAcknowledgedFalseOrderByCreatedAtDesc()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public AlertDto acknowledgeAlert(Long alertId) {
        Alert alert = alertRepository.findById(alertId)
                .orElseThrow(() -> new IllegalArgumentException("Alert not found"));
        alert.setAcknowledged(true);
        return toDTO(alertRepository.save(alert));
    }

    private AlertDto toDTO(Alert alert) {
        return new AlertDto(
                alert.getAlertId(),
                alert.getProject().getProjectId(),
                alert.getProject().getName(),
                alert.getSeverity().name(),
                alert.getMessage(),
                alert.isAcknowledged(),
                alert.getCreatedAt()
        );
    }
}