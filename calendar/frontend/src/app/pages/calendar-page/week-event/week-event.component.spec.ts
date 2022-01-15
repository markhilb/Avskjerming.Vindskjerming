import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WeekEventComponent } from './week-event.component';

describe('WeekEventComponent', () => {
  let component: WeekEventComponent;
  let fixture: ComponentFixture<WeekEventComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WeekEventComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WeekEventComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
