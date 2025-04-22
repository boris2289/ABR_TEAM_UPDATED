import { ComponentFixture, TestBed } from '@angular/core/testing';

import { YoutubeLinksComponent } from './youtube-links.component';

describe('YoutubeLinksComponent', () => {
  let component: YoutubeLinksComponent;
  let fixture: ComponentFixture<YoutubeLinksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [YoutubeLinksComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(YoutubeLinksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
