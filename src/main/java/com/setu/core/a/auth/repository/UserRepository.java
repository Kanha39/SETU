package com.setu.core.a.auth.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

import com.setu.core.a.auth.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
}