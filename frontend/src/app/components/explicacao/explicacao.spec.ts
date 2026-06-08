import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExplicacoesComponent } from './explicacao';

describe('Explicacao', () => {
  let component: ExplicacoesComponent;
  let fixture: ComponentFixture<ExplicacoesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExplicacoesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ExplicacoesComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
