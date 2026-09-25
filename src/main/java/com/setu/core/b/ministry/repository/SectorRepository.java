package com.setu.core.b.ministry.repository;

import com.setu.core.b.ministry.entity.Sector;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface SectorRepository extends JpaRepository<Sector, Long> {
    Optional<Sector> findByName(String name);
}