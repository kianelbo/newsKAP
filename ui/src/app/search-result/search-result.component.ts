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
  sortMethod = 'mostRelevant';
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
      this.page = 1;
      this.reSearch();
    });
  }

  doSearch() {
    this.router.navigateByUrl('/search?q=' + this.searchText);
  }

  reSearch() {
    this.newsService.getSearchResults(this.searchText, this.page, this.sortMethod).subscribe(res => {
      this.pageCount = Math.ceil(res.count / 10);
      this.results = res.data;
      this.noResult = this.results.length <= 0;
    }, err => {
      this.results = [];
      this.noResult = true;
    });
  }

  handleCategory(cat) {
    this.searchText += ' cat:' + cat;
    this.doSearch();
  }

}
