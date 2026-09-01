import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DespesasComponent } from './despesas';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';
import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';

registerLocaleData(localePt);

describe('Despesas', () => {
  let component: DespesasComponent;
  let fixture: ComponentFixture<DespesasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DespesasComponent],
      providers: [{ provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(DespesasComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
