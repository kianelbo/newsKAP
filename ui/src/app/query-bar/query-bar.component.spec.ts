import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { QueryBarComponent } from './query-bar.component';

describe('QueryBarComponent', () => {
  let component: QueryBarComponent;
  let fixture: ComponentFixture<QueryBarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ QueryBarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(QueryBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
