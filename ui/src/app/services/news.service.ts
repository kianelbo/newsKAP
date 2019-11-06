import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {NewsMiniModel} from '../models/news.mini.model';
import {NewsModel} from '../models/news.model';
import {NewsResponseModel} from '../models/news.response.model';

@Injectable({
  providedIn: 'root'
})
export class NewsService {
  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) { }

  getSearchResults(queryStr: string, page: number, sortMethod: string) {
    const r0 = (page - 1) * 10;
    const r1 = (page) * 10;
    return this.http.get<NewsResponseModel>
    (this.apiUrl + '/search?q=' + queryStr + '&r0=' + r0 + '&r1=' + r1 + '&sort=' + sortMethod);
  }

  getNews(id: string) {
    return this.http.get<NewsModel>(this.apiUrl + '/view/' + id);
  }
}
