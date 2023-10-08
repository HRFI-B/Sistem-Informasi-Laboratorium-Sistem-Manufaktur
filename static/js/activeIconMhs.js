function dashboard_active(){
    var element = document.getElementById("dashboard");
    element.classList.add("active");

    var element = document.getElementById("ruangan");
    element.classList.remove("active");

    var element = document.getElementById("arsip");
    element.classList.remove("active");
    
    var element = document.getElementById("alat");
    element.classList.remove("active");
    
    var element = document.getElementById("peminjaman");
    element.classList.remove("active");
}


function ruangan_active(){
    var element = document.getElementById("dashboard");
    element.classList.remove("active");

    var element = document.getElementById("ruangan");
    element.classList.add("active");

    var element = document.getElementById("arsip");
    element.classList.remove("active");
    
    var element = document.getElementById("alat");
    element.classList.remove("active");
    
    var element = document.getElementById("peminjaman");
    element.classList.remove("active");
}

function arsip_active(){
    var element = document.getElementById("dashboard");
    element.classList.remove("active");

    var element = document.getElementById("ruangan");
    element.classList.remove("active");

    var element = document.getElementById("arsip");
    element.classList.add("active");
    
    var element = document.getElementById("alat");
    element.classList.remove("active");
    
    var element = document.getElementById("peminjaman");
    element.classList.remove("active");
}

function alat_active(){
    var element = document.getElementById("dashboard");
    element.classList.remove("active");

    var element = document.getElementById("ruangan");
    element.classList.remove("active");

    var element = document.getElementById("arsip");
    element.classList.remove("active");
    
    var element = document.getElementById("alat");
    element.classList.add("active");

    var element = document.getElementById("peminjaman");
    element.classList.remove("active");
}

function peminjaman_active(){
    var element = document.getElementById("dashboard");
    element.classList.remove("active");

    var element = document.getElementById("ruangan");
    element.classList.remove("active");

    var element = document.getElementById("arsip");
    element.classList.remove("active");
    
    var element = document.getElementById("alat");
    element.classList.remove("active");
    
    var element = document.getElementById("peminjaman");
    element.classList.add("active");
}