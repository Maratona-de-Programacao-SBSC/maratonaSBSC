import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Voto } from './voto';

describe('Voto', () => {
  let component: Voto;
  let fixture: ComponentFixture<Voto>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Voto],
    }).compileComponents();

    fixture = TestBed.createComponent(Voto);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
