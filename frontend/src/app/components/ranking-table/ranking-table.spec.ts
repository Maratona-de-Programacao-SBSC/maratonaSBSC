import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RankingTableComponent } from './ranking-table';
import { provideRouter } from '@angular/router';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';

describe('RankingTable', () => {
  let component: RankingTableComponent;
  let fixture: ComponentFixture<RankingTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RankingTableComponent],
      providers: [provideRouter([]), { provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(RankingTableComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should classify alert levels', () => {
    expect(component.nivel(3)).toBe('Observação');
    expect(component.nivel(7)).toBe('Atenção');
    expect(component.nivel(15)).toBe('Alto');
    expect(component.nivel(20)).toBe('Crítico');
  });
});
