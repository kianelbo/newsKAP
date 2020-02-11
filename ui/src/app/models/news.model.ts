import { NewsMiniModel } from './news.mini.model';

export class NewsModel {
  date: string;
  title: string;
  source: string;
  summary: string;
  tags: string[];
  content: string;
  thumbnail: string;
  category: string;
  duplicates: NewsMiniModel[];
}
