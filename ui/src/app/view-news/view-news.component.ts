import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService, NewsFullView } from '../services/api.service';

@Component({
  selector: 'app-view-news',
  templateUrl: './view-news.component.html',
  styleUrls: ['./view-news.component.css']
})
export class ViewNewsComponent implements OnInit {
  news: NewsFullView;

  constructor(private route: ActivatedRoute,
              private apiService: ApiService) { }

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id');
    this.apiService.viewNews(id).subscribe(res => this.news = res);
  }

}
