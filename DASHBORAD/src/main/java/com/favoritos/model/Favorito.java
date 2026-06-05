package com.favoritos.model;

public class Favorito {

    private Long id;
    private String nome;
    private String url;
    private String grupo;

    public Favorito() {
    }

    public Favorito(Long id, String nome, String url, String grupo) {
        this.id = id;
        this.nome = nome;
        this.url = url;
        this.grupo = grupo;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getGrupo() {
        return grupo;
    }

    public void setGrupo(String grupo) {
        this.grupo = grupo;
    }
}