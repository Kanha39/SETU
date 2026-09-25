package com.setu.core.b.ministry.repository;

import com.setu.core.b.ministry.entity.Ministry;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface MinistryRepository extends JpaRepository<Ministry, Long> {
    Optional<Ministry> findByName(String name);
}