import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private searchURL = 'http://127.0.0.1:5000/search?q=';
  private viewURL = 'http://127.0.0.1:5000/view/';

  constructor(private http: HttpClient) { }

  getResults(queryStr: string) {
    return this.http.get<NewsMiniItem[]>(this.searchURL + queryStr);
  }

  viewNews(id: string) {
    return this.http.get<NewsFullView>(this.viewURL + id);
  }
}

export interface NewsMiniItem {
  date: string;
  title: string;
  source: string;
  preview: string;
  thumbnail: string;
  relevance: number;
  id: string;
}

export interface NewsFullView {
  date: string;
  title: string;
  source: string;
  summary: string;
  tags: string[];
  content: string;
  thumbnail: string;
}
