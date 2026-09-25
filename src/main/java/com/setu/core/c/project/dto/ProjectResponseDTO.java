package com.setu.core.c.project.dto;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

public class ProjectResponseDTO {

    private final Long projectId;
    private final String name;
    private final String ministryName;
    private final String sectorName;
    private final String implementingAgency;
    private final BigDecimal approvedCost;
    private final BigDecimal revisedCost;
    private final BigDecimal cumulativeExpenditure;
    private final LocalDate startDate;
    private final LocalDate scheduledEndDate;
    private final LocalDate revisedEndDate;
    private final Double physicalProgressPercent;
    private final String status;
    private final LocalDateTime lastUpdated;

    public ProjectResponseDTO(Long projectId, String name, String ministryName, String sectorName,
                              String implementingAgency, BigDecimal approvedCost, BigDecimal revisedCost,
                              BigDecimal cumulativeExpenditure, LocalDate startDate, LocalDate scheduledEndDate,
                              LocalDate revisedEndDate, Double physicalProgressPercent, String status,
                              LocalDateTime lastUpdated) {
        this.projectId = projectId;
        this.name = name;
        this.ministryName = ministryName;
        this.sectorName = sectorName;
        this.implementingAgency = implementingAgency;
        this.approvedCost = approvedCost;
        this.revisedCost = revisedCost;
        this.cumulativeExpenditure = cumulativeExpenditure;
        this.startDate = startDate;
        this.scheduledEndDate = scheduledEndDate;
        this.revisedEndDate = revisedEndDate;
        this.physicalProgressPercent = physicalProgressPercent;
        this.status = status;
        this.lastUpdated = lastUpdated;
    }

    public Long getProjectId() {
        return projectId;
    }

    public String getName() {
        return name;
    }

    public String getMinistryName() {
        return ministryName;
    }

    public String getSectorName() {
        return sectorName;
    }

    public String getImplementingAgency() {
        return implementingAgency;
    }

    public BigDecimal getApprovedCost() {
        return approvedCost;
    }

    public BigDecimal getRevisedCost() {
        return revisedCost;
    }

    public BigDecimal getCumulativeExpenditure() {
        return cumulativeExpenditure;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public LocalDate getScheduledEndDate() {
        return scheduledEndDate;
    }

    public LocalDate getRevisedEndDate() {
        return revisedEndDate;
    }

    public Double getPhysicalProgressPercent() {
        return physicalProgressPercent;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }
}