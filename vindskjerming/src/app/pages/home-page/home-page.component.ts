import { Component, OnInit, ViewChild, ChangeDetectorRef } from '@angular/core';

import { CanvasComponent } from '../../components/canvas/canvas.component';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
  standalone: false,
})
export class HomePageComponent implements OnInit {
  @ViewChild('canvas') canvas: CanvasComponent;

  customer: string;
  orderNumber: string;

  _totalWidthL: number;
  _totalWidthR: number;
  _globalWidth = 60;
  _globalHeight = 60;
  _leftMount = 'wallmount';
  _rightMount = 'post';
  _glassType = 'klart';

  transport = 'sendes';
  individualWidth = 60;
  individualHeight = 60;
  secondGlassHeight = 20;

  packageList = [];
  totalWeight: string;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    // Resize if needed before printing
    window.onbeforeprint = () => {
      // 700 = magic number (approx. width of a4 paper) 🤷
      const canvas = document.getElementById('canvas');
      if (canvas.offsetWidth > 700)
        canvas.style.zoom = (100 / (canvas.offsetWidth / 700)).toFixed(0) + '%';
    };

    // Reset page after printing
    window.onafterprint = () => {
      document.getElementById('canvas').style.zoom = '100%';
    };
  }

  get totalWidthL(): number {
    return this._totalWidthL;
  }

  set totalWidthL(val: number) {
    this._totalWidthL = val;
    this.canvas.setTotalWidthL(val);
  }

  get totalWidthR(): number {
    return this._totalWidthR;
  }

  set totalWidthR(val: number) {
    this._totalWidthR = val;
    this.canvas.setTotalWidthR(val);
  }

  get globalWidth(): number {
    return this._globalWidth;
  }

  set globalWidth(val: number) {
    this._globalWidth = val;
    this.canvas.setGlobalWidth(val);
  }

  get globalHeight(): number {
    return this._globalHeight;
  }

  set globalHeight(val: number) {
    this._globalHeight = val;
    this.canvas.setGlobalHeight(val);
  }

  get glassType(): string {
    return this._glassType;
  }

  set glassType(val: string) {
    this._glassType = val;
    this.canvas.setGlassType(val);
  }

  get leftMount(): string {
    return this._leftMount;
  }

  set leftMount(val: string) {
    this._leftMount = val;
    this.canvas.setLeftMount(val);
  }

  get rightMount(): string {
    return this._rightMount;
  }

  set rightMount(val: string) {
    this._rightMount = val;
    this.canvas.setRightMount(val);
  }

  get blob(): Blob {
    const body = JSON.stringify({
      _totalWidthL: this._totalWidthL,
      _totalWidthR: this._totalWidthR,
      _globalWidth: this._globalWidth,
      _globalHeight: this._globalHeight,
      _glassType: this._glassType,
      _leftMount: this._leftMount,
      _rightMount: this._rightMount,
      customer: this.customer,
      orderNumber: this.orderNumber,
      individualWidth: this.individualWidth,
      individualHeight: this.individualHeight,
      secondGlassHeight: this.secondGlassHeight,
      transport: this.transport,
      items: this.canvas.itemsAsJson(),
    });
    return new Blob([body], { type: 'text/plain;charset=utf-8' });
  }

  packageListChanged(event) {
    this.totalWeight = (event.weight / 1000).toFixed(0);
    this.packageList = event.list;
    this.cdr.detectChanges();
  }

  _fileSelected(text: string) {
    try {
      const json = JSON.parse(text);
      const items = json.items;
      delete json.items;
      Object.entries(json).forEach(([key, val]) => (this[key] = val));
      this.canvas.loadItems(items, this._totalWidthL, this._totalWidthR);
      (<HTMLInputElement>document.getElementById('fileInput')).value = null;
    } catch {}
  }

  fileSelected(event: Event) {
    const files = (event.target as HTMLInputElement).files;
    if (files.length === 1) {
      const fr = new FileReader();
      fr.onload = () => this._fileSelected(fr.result.toString());
      fr.readAsText(files[0]);
    }
  }

  onSave() {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(this.blob);
    a.download = this.orderNumber ? this.orderNumber : 'vindskjerming';
    a.click();
  }

  onLoad = () => document.getElementById('fileInput').click();

  onReset = () => this.canvas.clear();

  onUndo = () => this.canvas.undo();

  onAddWallmount = () => this.canvas.addWallmount();

  onAddPost = () => this.canvas.addPost();

  onAddGlass = () => this.canvas.addGlass();

  onAddGlassPolygon = () => this.canvas.addGlass(this.secondGlassHeight);
}
