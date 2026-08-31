import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotasComponent } from './notas';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';

describe('Notas', () => {
  let component: NotasComponent;
  let fixture: ComponentFixture<NotasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotasComponent],
      providers: [{ provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(NotasComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
