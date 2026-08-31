import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfosComponent } from './infos';
import { ApiService } from '../../services/api';
import { apiServiceMock } from '../../testing/api-service.mock';

describe('Infos', () => {
  let component: InfosComponent;
  let fixture: ComponentFixture<InfosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfosComponent],
      providers: [{ provide: ApiService, useValue: apiServiceMock }],
    }).compileComponents();

    fixture = TestBed.createComponent(InfosComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
