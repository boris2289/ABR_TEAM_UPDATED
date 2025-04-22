import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../auth.service'; 
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgIf, NgForOf } from '@angular/common';

@Component({
  selector: 'app-youtube-links',
  templateUrl: './youtube-links.component.html',
  styleUrls: ['./youtube-links.component.css'],
  imports: [FormsModule, NgIf, NgForOf]
})

export class YoutubeLinksComponent implements OnInit {
  newLink = { name: '', url: '', description: '', tags: '' };
  posts: any[] = [];
  toShow: boolean = false; 
  totalLinks: number | null = null;
  apiUrl = 'http://127.0.0.1:1278/api/youtube-links/';

  constructor(private http: HttpClient, private authService: AuthService) {
  }

  ngOnInit(): void {

  }

  createLink() {
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Token ${token}`);

    this.http.post(this.apiUrl, this.newLink, { headers }).subscribe(
      () => {
        this.fetchLinks();
        this.newLink = { name: '', url: '', description: '', tags: '' };
      },
      (error) => console.error('Error creating link:', error)
    );
  }

  fetchLinks() {

    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Token ${token}`);


    this.http.get<any[]>(this.apiUrl, { headers }).subscribe(
      (data) => {
        this.posts = data;
        this.toShow = true;  
        this.totalLinks = null;  
      },
      (error) => console.error('Error fetching links:', error)
    );
  }

  deleteLink(id: number) {
    const token = this.authService.getToken();
    const headers = new HttpHeaders().set('Authorization', `Token ${token}`);

    this.http.delete(`${this.apiUrl}${id}/`, { headers }).subscribe(
      () => {
        this.fetchLinks();
      },
      (error) => console.error('Error deleting link:', error)
    );
  }

  showTotalLinks() {
    this.http.get<any[]>(this.apiUrl).subscribe(
      (data) => {
        this.posts = data;
      },
      (error) => console.error('Error fetching links:', error)
    );
    if (this.toShow) {
      this.totalLinks = this.posts.length;
    }
  }

  hideLinks() {
    this.toShow = false;
    this.totalLinks = null; 
  }
}
