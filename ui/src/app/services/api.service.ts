import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private searchURL = 'http://127.0.0.1:5000/search?q=';

  constructor(private http: HttpClient) { }

  getResults(queryStr: string) {
    return this.http.get<News[]>(this.searchURL + queryStr);
  }
}

export interface News {
  date: string;
  title: string;
  source: string;
  summary: string;
  tags: string[];
  content: string;
  thumbnail: string;
  relevance: number;
}
