package com.setu.core.h.dashboard.dto;

import java.util.List;
import java.util.Map;

public class DashboardSummaryDTO {

    private final long totalProjects;
    private final Map<String, Long> projectsByStatus;
    private final Map<String, Long> projectsByRiskLevel;
    private final long activeAlertsCount;
    private final long criticalAlertsCount;
    private final List<TopRiskProjectDTO> topRiskProjects;

    public DashboardSummaryDTO(long totalProjects, Map<String, Long> projectsByStatus,
                               Map<String, Long> projectsByRiskLevel, long activeAlertsCount,
                               long criticalAlertsCount, List<TopRiskProjectDTO> topRiskProjects) {
        this.totalProjects = totalProjects;
        this.projectsByStatus = projectsByStatus;
        this.projectsByRiskLevel = projectsByRiskLevel;
        this.activeAlertsCount = activeAlertsCount;
        this.criticalAlertsCount = criticalAlertsCount;
        this.topRiskProjects = topRiskProjects;
    }

    public long getTotalProjects() {
        return totalProjects;
    }

    public Map<String, Long> getProjectsByStatus() {
        return projectsByStatus;
    }

    public Map<String, Long> getProjectsByRiskLevel() {
        return projectsByRiskLevel;
    }

    public long getActiveAlertsCount() {
        return activeAlertsCount;
    }

    public long getCriticalAlertsCount() {
        return criticalAlertsCount;
    }

    public List<TopRiskProjectDTO> getTopRiskProjects() {
        return topRiskProjects;
    }
}