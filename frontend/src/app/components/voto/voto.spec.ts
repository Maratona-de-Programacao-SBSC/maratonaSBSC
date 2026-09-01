import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VotoComponent } from './voto';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';

describe('VotoComponent', () => {
  let component: VotoComponent;
  let fixture: ComponentFixture<VotoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VotoComponent],
      providers: [{ provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(VotoComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
