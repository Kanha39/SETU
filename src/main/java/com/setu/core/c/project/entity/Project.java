package com.setu.core.c.project.entity;

import com.setu.core.b.ministry.entity.Ministry;
import com.setu.core.b.ministry.entity.Sector;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Entity
@Table(name = "projects")
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long projectId;

    @Column(nullable = false)
    private String name;

    @ManyToOne
    @JoinColumn(name = "ministry_id")
    private Ministry ministry;

    @ManyToOne
    @JoinColumn(name = "sector_id")
    private Sector sector;

    private String implementingAgency;

    private BigDecimal approvedCost;

    private BigDecimal revisedCost;

    private BigDecimal cumulativeExpenditure;

    private LocalDate startDate;

    private LocalDate scheduledEndDate;

    private LocalDate revisedEndDate;

    private Double physicalProgressPercent;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ProjectStatus status;

    private LocalDateTime lastUpdated;

    @PreUpdate
    @PrePersist
    protected void onUpdate() {
        this.lastUpdated = LocalDateTime.now();
    }

    public Long getProjectId() {
        return projectId;
    }

    public void setProjectId(Long projectId) {
        this.projectId = projectId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Ministry getMinistry() {
        return ministry;
    }

    public void setMinistry(Ministry ministry) {
        this.ministry = ministry;
    }

    public Sector getSector() {
        return sector;
    }

    public void setSector(Sector sector) {
        this.sector = sector;
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

    public ProjectStatus getStatus() {
        return status;
    }

    public void setStatus(ProjectStatus status) {
        this.status = status;
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(LocalDateTime lastUpdated) {
        this.lastUpdated = lastUpdated;
    }
}