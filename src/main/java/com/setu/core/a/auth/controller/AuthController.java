package com.setu.core.a.auth.controller;

import com.setu.core.a.auth.dto.RegisterRequest;
import com.setu.core.a.auth.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.setu.core.a.auth.dto.LoginResponse;
import com.setu.core.a.auth.dto.LoginRequest;
import com.setu.core.a.auth.entity.User;



@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@Valid @RequestBody RegisterRequest request) {
        User user = authService.register(request);
        return ResponseEntity.ok(user.getEmail() + " registered successfully");
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}