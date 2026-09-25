package com.setu.core.a.auth.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import com.setu.core.a.auth.repository.UserRepository;
import com.setu.core.a.auth.dto.RegisterRequest;
 import com.setu.core.a.auth.entity.User;
import com.setu.core.a.auth.entity.UserRole;
import com.setu.core.a.auth.entity.UserStatus;
import com.setu.core.a.auth.dto.LoginResponse;
import com.setu.core.a.auth.dto.LoginRequest;
import com.setu.core.a.auth.security.JwtUtil;
@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    public User register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email already registered");
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setRole(UserRole.USER);
        user.setStatus(UserStatus.ACTIVE);

        return userRepository.save(user);
    }

    public LoginResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("Invalid credentials"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid credentials");
        }

        String token = jwtUtil.generateToken(user.getEmail(), user.getRole().name());

        return new LoginResponse(token, user.getName(), user.getEmail(), user.getRole());
    }
}