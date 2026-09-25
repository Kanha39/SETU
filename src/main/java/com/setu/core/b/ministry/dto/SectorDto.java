package com.setu.core.b.ministry.dto;

import jakarta.validation.constraints.NotBlank;

public class SectorDto {

    private Long sectorId;

    @NotBlank
    private String name;

    public Long getSectorId() {
        return sectorId;
    }

    public void setSectorId(Long sectorId) {
        this.sectorId = sectorId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
