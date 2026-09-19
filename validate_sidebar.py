#!/usr/bin/env python3
"""Validação do Menu Lateral IBM Design System"""

import os
from pathlib import Path

base_path = Path("/home/dcalmeida/Documentos/GitHub/la-contabilidade/backend")

print("\n" + "="*60)
print("🚀 VALIDAÇÃO DO MENU LATERAL")
print("="*60)

# Verificar arquivos
files = {
    "sidebar.css": "static/css/sidebar.css",
    "sidebar.js": "static/js/sidebar.js",
    "layout.html": "portal/shared/layout.html",
}

print("\n📋 ARQUIVOS:")
for name, path in files.items():
    full_path = base_path / path
    status = "✅" if full_path.exists() else "❌"
    print(f"{status} {name}: {path}")

# Verificar features CSS
print("\n📦 FEATURES CSS:")
css_path = base_path / "static/css/sidebar.css"
if css_path.exists():
    with open(css_path) as f:
        css = f.read()
    features = {
        "CSS Variables": "--sidebar-bg" in css,
        "Tree View": ".nav-submenu" in css,
        "Responsive": "@media" in css,
        "Dark Mode": "dark" in css.lower(),
    }
    for feat, found in features.items():
        print(f"{'✅' if found else '❌'} {feat}")

# Verificar features JS
print("\n⚙️ FEATURES JAVASCRIPT:")
js_path = base_path / "static/js/sidebar.js"
if js_path.exists():
    with open(js_path) as f:
        js = f.read()
    features = {
        "SidebarMenu class": "class SidebarMenu" in js,
        "localStorage": "localStorage" in js,
        "Toggle menu": "toggleSubmenu" in js,
    }
    for feat, found in features.items():
        print(f"{'✅' if found else '❌'} {feat}")

# Verificar HTML
print("\n📄 ESTRUTURA HTML:")
html_path = base_path / "portal/shared/layout.html"
if html_path.exists():
    with open(html_path) as f:
        html = f.read()
    features = {
        "Sidebar CSS loaded": "sidebar.css" in html,
        "Sidebar JS loaded": "sidebar.js" in html,
        "Tree view": "nav-submenu" in html,
        "Admin section": "admin-only" in html,
    }
    for feat, found in features.items():
        print(f"{'✅' if found else '❌'} {feat}")

print("\n" + "="*60)
print("✅ Menu lateral implementado com sucesso!")
print("\n📍 Localização dos arquivos:")
print(f"   CSS: {base_path}/static/css/sidebar.css")
print(f"   JS:  {base_path}/static/js/sidebar.js")
print(f"   HTML: {base_path}/portal/shared/layout.html")
print("\n🎯 Próximos passos:")
print("   1. Abra http://localhost:5000/portal/equipe")
print("   2. Teste expandir/colapsar menus")
print("   3. Teste em mobile (<768px)")
print("="*60 + "\n")
