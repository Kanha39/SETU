package com.setu.core.c.project.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;
import java.time.LocalDate;

public class ProjectRequestDTO {

    @NotBlank
    private String name;

    private Long ministryId;

    private Long sectorId;

    private String implementingAgency;

    @NotNull
    private BigDecimal approvedCost;

    private BigDecimal revisedCost;

    private BigDecimal cumulativeExpenditure;

    private LocalDate startDate;

    private LocalDate scheduledEndDate;

    private LocalDate revisedEndDate;

    private Double physicalProgressPercent;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Long getMinistryId() {
        return ministryId;
    }

    public void setMinistryId(Long ministryId) {
        this.ministryId = ministryId;
    }

    public Long getSectorId() {
        return sectorId;
    }

    public void setSectorId(Long sectorId) {
        this.sectorId = sectorId;
    }

    public String getImplementingAgency() {
        return implementingAgency;
    }

    public void setImplementingAgency(String implementingAgency) {
        this.implementingAgency = implementingAgency;
    }

    public BigDecimal getApprovedCost() {
        return approvedCost;
    }

    public void setApprovedCost(BigDecimal approvedCost) {
        this.approvedCost = approvedCost;
    }

    public BigDecimal getRevisedCost() {
        return revisedCost;
    }

    public void setRevisedCost(BigDecimal revisedCost) {
        this.revisedCost = revisedCost;
    }

    public BigDecimal getCumulativeExpenditure() {
        return cumulativeExpenditure;
    }

    public void setCumulativeExpenditure(BigDecimal cumulativeExpenditure) {
        this.cumulativeExpenditure = cumulativeExpenditure;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getScheduledEndDate() {
        return scheduledEndDate;
    }

    public void setScheduledEndDate(LocalDate scheduledEndDate) {
        this.scheduledEndDate = scheduledEndDate;
    }

    public LocalDate getRevisedEndDate() {
        return revisedEndDate;
    }

    public void setRevisedEndDate(LocalDate revisedEndDate) {
        this.revisedEndDate = revisedEndDate;
    }

    public Double getPhysicalProgressPercent() {
        return physicalProgressPercent;
    }

    public void setPhysicalProgressPercent(Double physicalProgressPercent) {
        this.physicalProgressPercent = physicalProgressPercent;
    }
}