import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="layout">
      <aside class="sidebar">
        <div class="brand">
          <span class="brand-icon">⚖</span>
          <span class="brand-name">AuditGov</span>
        </div>
        <nav>
          <a routerLink="/dashboard" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">◈</span> Dashboard
          </a>
          <a routerLink="/notas" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">◉</span> Notas Fiscais
          </a>
          <a routerLink="/despesas" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">◎</span> Despesas
          </a>
        </nav>
        <div class="sidebar-footer">
          Portal da Transparência
        </div>
      </aside>
      <main class="main-content">
        <router-outlet />
      </main>
    </div>
  `,
})
export class AppComponent {}