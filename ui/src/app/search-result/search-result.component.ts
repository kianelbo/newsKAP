import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {NewsService} from '../services/news.service';
import {NewsMiniModel} from '../models/news.mini.model';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit {
  searchText = '';
  sortMethod = 'newest';
  results: NewsMiniModel[];
  noResult = true;
  page = 1;
  pageCount = 0;

  constructor(private route: ActivatedRoute,
              private router: Router,
              private newsService: NewsService) {
  }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.searchText = params['q'];
      this.reSearch();
    });
  }

  doSearch() {
    this.router.navigateByUrl('/search?q=' + this.searchText);
  }

  reSearch() {
    this.newsService.getSearchResults(this.searchText, this.page, this.sortMethod).subscribe(res => {
      console.log('result count:' + res.count);
      this.pageCount = Math.floor(res.count / 10) + 1;
      this.results = res.data;
      this.noResult = false;
    }, err => {
      this.noResult = true;
    });
  }

}
