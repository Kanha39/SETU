package com.setu.core.h.dashboard.service;

import com.setu.core.c.project.entity.ProjectStatus;
import com.setu.core.c.project.repository.ProjectRepository;
import com.setu.core.e.risk.entity.RiskLevel;
import com.setu.core.e.risk.entity.RiskScore;
import com.setu.core.e.risk.repository.RiskScoreRepository;
import com.setu.core.g.alert.entity.AlertSeverity;
import com.setu.core.h.dashboard.dto.DashboardSummaryDTO;
import com.setu.core.h.dashboard.dto.TopRiskProjectDTO;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import com.setu.core.g.alert.repository.AlertRepository;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class DashboardService {

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private RiskScoreRepository riskScoreRepository;

    @Autowired
    private AlertRepository alertRepository;

    public DashboardSummaryDTO getSummary() {
        long totalProjects = projectRepository.count();

        Map<String, Long> projectsByStatus = new LinkedHashMap<>();
        for (ProjectStatus status : ProjectStatus.values()) {
            projectsByStatus.put(status.name(), (long) projectRepository.findByStatus(status).size());
        }

        Map<String, Long> projectsByRiskLevel = new LinkedHashMap<>();
        for (RiskLevel level : RiskLevel.values()) {
            projectsByRiskLevel.put(level.name(), riskScoreRepository.countByRiskLevel(level));
        }

        long activeAlertsCount = alertRepository.countByAcknowledgedFalse();
        long criticalAlertsCount = alertRepository.countBySeverityAndAcknowledgedFalse(AlertSeverity.CRITICAL);

        List<RiskScore> topScores = riskScoreRepository
                .findLatestScoresOrderedByValueDesc(PageRequest.of(0, 5));

        List<TopRiskProjectDTO> topRiskProjects = topScores.stream()
                .map(r -> new TopRiskProjectDTO(
                        r.getProject().getProjectId(),
                        r.getProject().getName(),
                        r.getRiskScoreValue(),
                        r.getRiskLevel().name()
                ))
                .collect(Collectors.toList());

        return new DashboardSummaryDTO(totalProjects, projectsByStatus, projectsByRiskLevel,
                activeAlertsCount, criticalAlertsCount, topRiskProjects);
    }
}