import {Component, Input, OnInit} from '@angular/core';
import {NewsModel} from '../models/news.model';
import {NewsService} from '../services/news.service';

@Component({
  selector: 'app-news-summary',
  templateUrl: './news-summary.component.html',
  styleUrls: ['./news-summary.component.scss']
})
export class NewsSummaryComponent implements OnInit {
  news: NewsModel;

  constructor(private newsService: NewsService) { }

  ngOnInit() {
  }

  reload(id: string) {
    this.news = null;
    console.log('getting id:' + id);
    this.newsService.getNews(id).subscribe(res => {
      console.log(res);
      this.news = res;
    });
  }

}
