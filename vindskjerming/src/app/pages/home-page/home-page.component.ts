import { Component, OnInit, ViewChild, ChangeDetectorRef } from '@angular/core';

import { CanvasComponent } from '../../components/canvas/canvas.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  @ViewChild('canvas') canvas: CanvasComponent;

  totalWidthL: number;
  totalWidthR: number;
  customer: string;
  orderNumber: string;

  glassType = 'klart';
  leftMount = 'wallmount';
  rightMount = 'post';
  globalWidth = 60;
  globalHeight = 60;
  transport = 'sendes';

  individualWidth = 60;
  individualHeight = 60;
  secondGlassHeight: number;

  packageList = [];
  totalWeight: string;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {}

  updatePackageList(event) {
    this.totalWeight = (event.weight / 1000).toFixed(0);
    delete event.weight;
    this.packageList = [];
    Object.entries(event).map(([key, val]) => {
      Object.entries(val).map(([size, num]) => {
        this.packageList.push([key, size, num]);
        key = '';
      });
    });
    this.cdr.detectChanges();
  }

  onSave() {
    // TODO
    // console.log('Save...');
  }

  onLoad() {
    // TODO
    // console.log('Load...');
  }

  onReset = () => this.canvas.clear();

  onUndo = () => this.canvas.undo();

  onAddWallmount = () => this.canvas.addWallmount();

  onAddPost = () => this.canvas.addPost();

  onAddGlass = () => this.canvas.addGlass();

  onAddGlassPolygon = () => this.canvas.addGlass(this.secondGlassHeight);
}
