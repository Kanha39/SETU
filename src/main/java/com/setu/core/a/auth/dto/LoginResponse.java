package com.setu.core.a.auth.dto;
 import com.setu.core.a.auth.entity.UserRole;


public class LoginResponse {

    private String token;
    private String name;
    private String email;
    private UserRole role;

    public LoginResponse(String token, String name, String email, UserRole role) {
        this.token = token;
        this.name = name;
        this.email = email;
        this.role = role;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public UserRole getRole() {
        return role;
    }

    public void setRole(UserRole role) {
        this.role = role;
    }
}