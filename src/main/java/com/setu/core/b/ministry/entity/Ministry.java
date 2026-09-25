package com.setu.core.b.ministry.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "ministries")
public class Ministry {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long ministryId;

    @Column(nullable = false, unique = true)
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