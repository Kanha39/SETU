package com.setu.core.b.ministry.service;

import com.setu.core.b.ministry.dto.SectorDto;
import com.setu.core.b.ministry.entity.Ministry;
import com.setu.core.b.ministry.entity.Sector;
import com.setu.core.b.ministry.repository.MinistryRepository;
import com.setu.core.b.ministry.repository.SectorRepository;
import com.setu.core.b.ministry.dto.MinistryDto;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class MinistryService {

    @Autowired
    private MinistryRepository ministryRepository;

    @Autowired
    private SectorRepository sectorRepository;

    public MinistryDto createMinistry(MinistryDto dto) {
        Ministry ministry = new Ministry();
        ministry.setName(dto.getName());
        ministry.setDepartment(dto.getDepartment());
        return toDTO(ministryRepository.save(ministry));
    }

    public List<MinistryDto> getAllMinistries() {
        return ministryRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public SectorDto createSector(SectorDto dto) {
        Sector sector = new Sector();
        sector.setName(dto.getName());
        return toDTO(sectorRepository.save(sector));
    }

    public List<SectorDto> getAllSectors() {
        return sectorRepository.findAll()
                .stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private MinistryDto toDTO(Ministry ministry) {
        MinistryDto dto = new MinistryDto();
        dto.setMinistryId(ministry.getMinistryId());
        dto.setName(ministry.getName());
        dto.setDepartment(ministry.getDepartment());
        return dto;
    }

    private SectorDto toDTO(Sector sector) {
        SectorDto dto = new SectorDto();
        dto.setSectorId(sector.getSectorId());
        dto.setName(sector.getName());
        return dto;
    }
}