package com.setu.core.b.ministry.dto;

import jakarta.validation.constraints.NotBlank;

public class MinistryDto {

    private Long ministryId;

    @NotBlank
    private String name;

    private String department;

    public Long getMinistryId() {
        return ministryId;
    }

    public void setMinistryId(Long ministryId) {
        this.ministryId = ministryId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }
}
